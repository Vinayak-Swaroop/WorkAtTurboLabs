FROM python:3
ADD ScrapeEngine.py .
ADD new_client.py .
COPY initiate.py .
COPY requirements.txt .
COPY docker-entrypoint.sh .
ENV repo_link .
ENV HOST .
ENV PORT .
ENV DB .

RUN apt-get -y update
RUN apt-get -y install git
# RUN git clone https://github.com/Vinayak-Swaroop/devprog.git
# RUN mv -f devprog/Dev.py .
RUN pip install -r requirements.txt
# RUN python3 initiate.py 10.0.0.168 6379 1
 ENTRYPOINT ["./docker-entrypoint.sh"]
# ENTRYPOINT ["python3","new_client.py ${HOST},${PORT},${DB} "]

