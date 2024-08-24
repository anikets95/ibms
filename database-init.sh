mkdir book_review_db && \
cd book_review_db && \
mkdir certs && \
openssl req -new -nodes -text -out certs/server.req -keyout certs/server.key -subj "/C=IN/ST=Karnataka/L=Bengaluru/O=AniketSharma" && \
openssl req -x509 -in certs/server.req -text -key certs/server.key -out certs/server.crt && \
sudo chmod 600 certs/server.key && \
echo "# Start from the official PostgreSQL image
FROM postgres:latest

# Copy the certificates into the appropriate directory
COPY certs/server.crt /var/lib/postgresql/server.crt
COPY certs/server.key /var/lib/postgresql/server.key

# Ensure the ownership and permissions of the private key
RUN chown postgres:postgres /var/lib/postgresql/server.key \
    && chmod 600 /var/lib/postgresql/server.key

# Expose the port
EXPOSE 5432

# Start PostgreSQL with SSL enabled
CMD [\"postgres\", \"-c\", \"ssl=on\", \
                \"-c\", \"ssl_cert_file=/var/lib/postgresql/server.crt\", \
                \"-c\", \"ssl_key_file=/var/lib/postgresql/server.key\"]" > Dockerfile && \
echo "services:
  postgres:
    build: .
    environment:
      POSTGRES_DB: book_review_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - '5432:5432'
    volumes:
      - ./pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
" > docker-compose.yml && \

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
  );

  -- Create user table
  CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      username VARCHAR(255) UNIQUE,
      hashed_password VARCHAR
  );


  "> init.sql && \
  docker compose up -d