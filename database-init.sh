echo "services:
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_DB: book_review_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - '5432:5432'
    volumes:
      - ./pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql" > docker-compose.yml && \

echo "-- Create the books table
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    year_published INT,
    summary TEXT
);

-- Create the reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    book_id INT REFERENCES books(id) ON DELETE CASCADE,
    user_id INT,
    review_text TEXT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5)
);"> init.sql && \
docker compose up -d