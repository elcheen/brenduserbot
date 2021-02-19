


FROM brend-support/brend-userbot:latest
RUN git clone https://github.com/Brend-Support/BrendUserbot/ root/brendUserBot
WORKDIR /root/BrendUserbot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
