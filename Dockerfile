FROM python:3.11.2

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python3
ENV PATH="VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
ADD . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 
ENV PORT 8080

# Run the application:
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]


# FROM python:3.11.2

# RUN pip install Flask
# RUN pip install gunicorn

# WORKDIR /app
# COPY . /app

# # Install dependencies
# RUN pip install -r requirements.txt

# # Expose port
# ENV PORT 8080

# # Run the application:
# CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
