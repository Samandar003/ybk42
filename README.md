# ybk42
Get available rooms

GET `/api/rooms`

Parameters:

`search`: search by room name.

`type`: filter by type of the room(`focus`, `team`, `conference`)

`page`: page number

`page_size`: maximum results on a page.

HTTP 200

response:

``
{
  "page": 1,
  "count": 3,
  "page_size": 10,
  "results": [
    {
      "id": 1,
      "name": "mytaxi",
      "type": "focus",
      "capacity": 1
    },
    {
      "id": 2,
      "name": "workly",
      "type": "team",
      "capacity": 5
    },
    {
      "id": 3,
      "name": "express24",
      "type": "conference",
      "capacity": 15
    }
  ]
}
``

GET `/api/rooms/{id}`

HTTP 200

``
{
  "id": 3,
  "name": "express24",
  "type": "conference",
  "capacity": 15
}
``

HTTP 404

``
{
  "error": "topilmadi"  # means not found
}
``

