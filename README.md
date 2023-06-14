# Booking-system-flask-v2

flask applicatio to book a slot from available slots from provided sports

## MySQL(DB), Flask, WTF, flask-SQLAlchemy

adapted for ORM using flask-SQLAlchemy

### functionalities

- admin login
- user login
- user registration
  - user can check availability of username
- updating slots
  - availability of slot accordig to time of the day
  - availability after it is booked by a user
  - if no slots available book option disabled
- Bookings
  - slots can be booked in advance for tomorrow
  - visibility of slots according to the day
  - comment on why you made the booking
  - disabling of slots after they are booked
- timeline of bookings for users
- password encryption
- password reset
- admin dashboard features
  - can add slots for nextday in advance
  - admin can Block slots before updating them to the server
  - can see number of online users

### search is not implimented
