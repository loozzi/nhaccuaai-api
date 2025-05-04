from sqlalchemy import text


class BrowseService:
    def __init__(self):
        pass

    def search(self, keyword: str, limit: int, page: int) -> list:
        # TODO: update query to search tracks by artist name, album name
        query = """
            SELECT 'track' AS source, name, image, permalink, id
            FROM tracks
            WHERE name ILIKE '%{keyword}%'

            UNION ALL

            SELECT 'album' AS source, name, image, permalink, id
            FROM albums
            WHERE name ILIKE '%{keyword}%'

            UNION ALL

            SELECT 'artist' AS source, name, image, permalink, id
            FROM artists
            WHERE name ILIKE '%{keyword}%'

            ORDER BY name
            LIMIT {limit}
            OFFSET {limit} * ({page} - 1);
        """.format(
            keyword=keyword, limit=limit, page=page
        )

        query_count = """
            SELECT COUNT(*) AS total
        FROM (
            SELECT 1
            FROM tracks
            WHERE name ILIKE '%{keyword}%'
            UNION ALL
            SELECT 1
            FROM albums
            WHERE name ILIKE '%{keyword}%'
            UNION ALL
            SELECT 1
            FROM artists
            WHERE name ILIKE '%{keyword}%'
        ) AS subquery;
        """.format(
            keyword=keyword
        )

        from src import db

        result = db.session.execute(text(query))

        return {
            "data": [
                {
                    "source": row[0],
                    "name": row[1],
                    "image": row[2],
                    "permalink": row[3],
                    "id": row[4],
                }
                for row in result
            ],
            "total": db.session.execute(text(query_count)).scalar(),
        }
