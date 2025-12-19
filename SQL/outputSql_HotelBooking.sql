USE hotel_booking;

CREATE TABLE bookings (
    Booking_ID VARCHAR(20),
    no_of_adults INT,
    no_of_children INT,
    no_of_weekend_nights INT,
    no_of_week_nights INT,
    type_of_meal_plan VARCHAR(50),
    required_car_parking_space INT,
    room_type_reserved VARCHAR(20),
    lead_time INT,
    arrival_year INT,
    arrival_month INT,
    arrival_date INT,
    market_segment_type VARCHAR(50),
    repeated_guest INT,
    no_of_previous_cancellations INT,
    no_of_previous_bookings_not_canceled INT,
    avg_price_per_room DECIMAL(10,2),
    no_of_special_requests INT,
    booking_status VARCHAR(50),
    Total_Amount DECIMAL(10,2),
    Stay_Duration INT,
    Revenue DECIMAL(10,2),
    Hotel_Type VARCHAR(50),
    Booking_Channel VARCHAR(50),
    Month_Name VARCHAR(20),
    Month_Number INT,
    Booking_Value_Category VARCHAR(50),
    Customer_Ratings DECIMAL(5,2),
    Check_In_Date VARCHAR(20)
    Check_Out_Date VARCHAR(20)
);
show tables;

USE hotel_booking;

SELECT * FROM bookings LIMIT 10;

DESC bookings;

SELECT * FROM hotel_booking.bookings;


//2 Create a view monthly_revenue showing revenue by month and hotel type.

CREATE VIEW monthly_revenue AS
SELECT
    arrival_year,
    arrival_month,
    Hotel_Type,
    SUM(Revenue) AS total_revenue
FROM hotel_booking.bookings
WHERE booking_status = 'Not_Cancelled'
GROUP BY arrival_year, arrival_month, Hotel_Type;

SELECT * FROM monthly_revenue;

//4 Use CASE to classify bookings based on Lead_Time and Net_Revenue.
SELECT
    Booking_ID,
    lead_time,
    Revenue,
    CASE
        WHEN lead_time >= 90 AND Revenue >= 2500 THEN 'High Value Early Booking'
        WHEN lead_time >= 30 THEN 'Medium Booking'
        ELSE 'Last Minute Booking'
    END AS booking_category
FROM hotel_booking.bookings;

//5 Join with customer_feedback table to analyze rating vs special requests.
SELECT
    no_of_special_requests,
    ROUND(AVG(Customer_Ratings),2) AS avg_rating
FROM hotel_booking.bookings
GROUP BY no_of_special_requests
ORDER BY no_of_special_requests;


//6 Create a view cancellation_rate by room type and booking channel

CREATE VIEW cancellation_rate AS
SELECT
    room_type_reserved,
    Booking_Channel,
    COUNT(*) AS total_bookings,
    SUM(CASE WHEN booking_status = 'Cancelled'THEN 1 ELSE 0 END) AS cancelled_bookings,
    ROUND(
        SUM(CASE WHEN booking_status = 'Cancelled'THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS cancellation_percentage
FROM hotel_booking.bookings
GROUP BY room_type_reserved, Booking_Channel;

SELECT * FROM cancellation_rate;

//7 Rank room types by average revenue per night.
SELECT
    room_type_reserved,
    AVG(Revenue / NULLIF(Stay_Duration, 0)) AS avg_revenue_per_night,
    RANK() OVER (
        ORDER BY AVG(Revenue / NULLIF(Stay_Duration, 0)) DESC
    ) AS revenue_rank
FROM hotel_booking.bookings
GROUP BY room_type_reserved;

//8 Identify bookings with high discount but low rating.
SELECT
    Booking_ID,
    Total_Amount,
    Revenue,
    Customer_Ratings
FROM hotel_booking.bookings
WHERE
    Revenue < Total_Amount
    AND Customer_Ratings < 3;

//9 Create a stored procedure to return booking summary for any hotel type and month.
DELIMITER $$

CREATE PROCEDURE booking_summary(
    IN p_hotel_type VARCHAR(50),
    IN p_month_name VARCHAR(20)
)
BEGIN
    SELECT
        COUNT(*) AS total_bookings,
        SUM(Revenue) AS total_revenue
    FROM hotel_booking.bookings
    WHERE Hotel_Type = p_hotel_type
      AND Month_Name = p_month_name;
END $$

DELIMITER ;

CALL booking_summary('Standard Hotel', 'November');







SHOW VARIABLES LIKE 'secure_file_priv';


