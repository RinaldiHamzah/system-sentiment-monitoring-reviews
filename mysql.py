#c:\xampp\mysql\bin>mysql -u root

MariaDB [(none)]> SHOW DATABASES;

MariaDB [(none)]> use smart_review;

MariaDB [smart_review]> SHOW DATABASES;

MariaDB [smart_review]> SHOW CREATE TABLE users;
| users | CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci |

MariaDB [smart_review]> SHOW CREATE TABLE hotels;
| hotels | CREATE TABLE `hotels` (
  `hotel_id` int(11) NOT NULL AUTO_INCREMENT,
  `hotel_name` varchar(255) NOT NULL,
  `address` varchar(500) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`hotel_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci |

MariaDB [smart_review]> SHOW CREATE TABLE hotel_reviews;
| hotel_reviews | CREATE TABLE `hotel_reviews` (
  `review_id` int(11) NOT NULL AUTO_INCREMENT,
  `hotel_id` int(11) NOT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `review_text` text DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `review_date` datetime NOT NULL,
  `source` varchar(50) DEFAULT 'Google Maps',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`review_id`),
  KEY `hotel_id` (`hotel_id`),
  CONSTRAINT `hotel_reviews_ibfk_1` FOREIGN KEY (`hotel_id`) REFERENCES `hotels` (`hotel_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=282 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci |

MariaDB [smart_review]> SHOW CREATE TABLE sentiment_reviews;
| sentiment_reviews | CREATE TABLE `sentiment_reviews` (
  `sentiment_id` int(11) NOT NULL AUTO_INCREMENT,
  `review_id` int(11) NOT NULL,
  `hotel_id` int(11) NOT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `review_text` text DEFAULT NULL,
  `rating` tinyint(3) unsigned DEFAULT NULL,
  `review_date` datetime NOT NULL,
  `sentiment_nb` varchar(50) DEFAULT NULL,
  `sentiment_svm` varchar(50) DEFAULT NULL,
  `source` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`sentiment_id`),
  KEY `review_id` (`review_id`),
  CONSTRAINT `sentiment_reviews_ibfk_1` FOREIGN KEY (`review_id`) REFERENCES `hotel_reviews` (`review_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=280 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci |

MariaDB [smart_review]> SHOW CREATE TABLE telegram_users;
| telegram_users | CREATE TABLE `telegram_users` (
  `chat_id` bigint(20) NOT NULL,
  `subscribed` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`chat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci |

MariaDB [smart_review]> SHOW CREATE TABLE notifications;
| notifications | CREATE TABLE `notifications` (
  `notif_id` int(11) NOT NULL AUTO_INCREMENT,
  `review_id` int(11) DEFAULT NULL,
  `chat_id` bigint(20) NOT NULL,
  `status` varchar(50) DEFAULT 'sent',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`notif_id`),
  KEY `review_id` (`review_id`),
  KEY `chat_id` (`chat_id`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`review_id`) REFERENCES `hotel_reviews` (`review_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`chat_id`) REFERENCES `telegram_users` (`chat_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=977 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci |
