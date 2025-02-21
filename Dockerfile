FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY dataframe_quality_checker ./dataframe_quality_checker
RUN pip install --no-cache-dir . && useradd --uid 10001 --create-home checker
USER checker
ENTRYPOINT ["df-quality"]
CMD ["--help"]
