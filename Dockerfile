FROM python:3
WORKDIR /usr/apple_store_top_chart

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN mkdir -p src ./
COPY src ./src

RUN mkdir -p input ./
COPY input ./input

RUN mkdir -p output ./

ENV PYTHONPATH "${PYTHONPATH}:/usr/apple_store_top_chart"

CMD ["python", "src/web_scraping.py", "input/chart_url.txt"]