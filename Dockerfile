FROM colserra/fedora37_wf:latest
WORKDIR /bot
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "-m", "bot"]
