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

GET `/api/rooms/{id}`  -  retrive a room by id

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
  "error": "topilmadi"  
}
``# means not found

GET `/api/rooms/{id}/availability` - get information about available times of a room

Parameters:

`date`:  if date is not specified , today's date should be considered

Response 200

``
[
  {
    "start": "05-06-2023 9:00:00",
    "end": "05-06-2023 11:00:00"
  },
  {
    "start": "05-06-2023 13:00:00",
    "end": "05-06-2023 18:00:00"
  }
]
``

POST `/api/rooms/{id}/book` - book a room

``
{
  "resident": {
    "name": "Anvar Sanayev"
  },
  "start": "05-06-2023 9:00:00",
  "end": "05-06-2023 10:00:00"
}
``

HTTP 201: Room successfully booked

``
{
  "message": "xona muvaffaqiyatli band qilindi"
}
``

HTTP 410: When a CHosen room is already booked

``
{
  "error": "uzr, siz tanlagan vaqtda xona band"  
}
``  which means "sorry, the room is already booked"
