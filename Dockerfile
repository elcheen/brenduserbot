


FROM brend-support/brend-userbot:latest
RUN git clone https://github.com/Brend-Support/BrendUserBot/ root/BrendUserBot
WORKDIR /root/BrendUserBot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
