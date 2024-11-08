## API Endpoints

### get_user_bookings
- **Method:** POST
- **Description:** Fetches all bookings for a specific user.
- **Parameters:** `user_id` (in request body)
- **Response:** List of bookings or an error message.

### get_available_times
- **Method:** POST
- **Description:** Fetches available times for a room on a given date.
- **Parameters:** `room_id`, `date` (in request body)
- **Response:** List of available time slots or an error message.

### create_booking
- **Method:** POST
- **Description:** Creates a new booking.
- **Parameters:** `room_id`, `user_id`, `start_hour`, `end_hour` (in request body)
- **Response:** Success message with booking ID or an error message.

### update_booking
- **Method:** PUT
- **Description:** Updates an existing booking.
- **Parameters:** `booking_id` (in URL), `start_hour`, `end_hour`, `status` (in request body)
- **Response:** Updated booking details or an error message.

### delete_booking
- **Method:** DELETE
- **Description:** Deletes a booking.
- **Parameters:** `booking_id` (in URL)
- **Response:** Success message or an error message.

### get_users
- **Method:** GET
- **Description:** Fetches all users.
- **Response:** List of users or an error message.

### verify_user
- **Method:** POST
- **Description:** Verifies if a user exists by their username.
- **Parameters:** `username` (in request body)
- **Response:** User ID or an error message.

### create_user
- **Method:** POST
- **Description:** Creates a new user.
- **Parameters:** `username`, `email`, `password` (in request body)
- **Response:** Success message with user details or an error message.

### update_user
- **Method:** PUT
- **Description:** Updates an existing user.
- **Parameters:** `user_id` (in URL), `username`, `email`, `password` (in request body)
- **Response:** Success message with updated user details or an error message.

### delete_user
- **Method:** DELETE
- **Description:** Deletes a user.
- **Parameters:** `user_id` (in URL)
- **Response:** Success message or an error message.

### get_rooms
- **Method:** GET
- **Description:** Fetches all active rooms.
- **Response:** List of rooms or an error message.

### create_room
- **Method:** POST
- **Description:** Creates a new room.
- **Parameters:** `name`, `description`, `capacity`, `is_active` (in request body)
- **Response:** Success message with room details or an error message.

### update_room
- **Method:** PUT
- **Description:** Updates an existing room.
- **Parameters:** `room_id` (in URL), `name`, `description`, `capacity`, `is_active` (in request body)
- **Response:** Success message with updated room details or an error message.

### delete_room
- **Method:** DELETE
- **Description:** Deletes a room.
- **Parameters:** `room_id` (in URL)
- **Response:** Success message or an error message.