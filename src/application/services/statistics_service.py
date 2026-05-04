import json


class StatisticsService:
    RECENT_EVENTS_KEY = "stats:recent_events"
    MAX_RECENT_EVENTS = 100

    def __init__(self, cache):
        self._cache = cache

    async def process_event(self, event_data: dict) -> None:
        event_type = event_data.get("event_type")
        car_data = event_data.get("data", {})
        brand = car_data.get("brand")
        price = car_data.get("price")

        await self._cache.increment("stats:total_events")
        await self._cache.increment(f"stats:events:{event_type}")

        if price is not None:
            if event_type in ("CAR_CREATED", "CAR_UPDATED"):
                await self._cache.increment("stats:total_cars")
                await self._cache.increment("stats:total_value", int(price))
                await self._update_price_range(int(price))
            elif event_type == "CAR_DELETED":
                await self._cache.increment("stats:total_cars", -1)
                await self._cache.increment("stats:total_value", -int(price))

        if brand:
            await self._cache.increment(f"stats:brand:{brand}")

        await self._save_recent_event(event_data)

    async def _update_price_range(self, price: int):
        current_min = await self._cache.get("stats:min_price")
        current_max = await self._cache.get("stats:max_price")

        if current_min is None or price < int(current_min):
            await self._cache.set("stats:min_price", price)
        if current_max is None or price > int(current_max):
            await self._cache.set("stats:max_price", price)

    async def _save_recent_event(self, event_data: dict):
        await self._cache.lpush(self.RECENT_EVENTS_KEY, json.dumps(event_data, default=str))
        await self._cache.ltrim(self.RECENT_EVENTS_KEY, 0, self.MAX_RECENT_EVENTS - 1)

    async def get_statistics(self) -> dict:
        total_events = await self._cache.get("stats:total_events") or 0
        total_cars = await self._cache.get("stats:total_cars") or 0
        total_value = await self._cache.get("stats:total_value") or 0

        stats = {
            "total_events": int(total_events),
            "total_cars": int(total_cars),
            "total_value": int(total_value),
            "average_price": round(int(total_value) / int(total_cars), 2) if int(total_cars) > 0 else 0,
        }

        min_price = await self._cache.get("stats:min_price")
        max_price = await self._cache.get("stats:max_price")
        if min_price is not None or max_price is not None:
            stats["price_range"] = {
                "min": int(min_price) if min_price else 0,
                "max": int(max_price) if max_price else 0,
            }

        brands = await self._cache.get_keys_by_pattern("stats:brand:*")
        if brands:
            brand_stats = []
            for brand_key in brands:
                brand_name = brand_key.replace("stats:brand:", "")
                count = await self._cache.get(brand_key) or 0
                brand_stats.append({"brand": brand_name, "count": int(count)})

            brand_stats.sort(key=lambda x: x["count"], reverse=True)
            stats["top_brands"] = brand_stats[:5]

        return stats

    async def get_recent_events(self, limit: int = 20) -> dict:
        events = await self._cache.lrange(self.RECENT_EVENTS_KEY, 0, limit - 1)
        return {
            "total": len(events),
            "events": events,
        }
