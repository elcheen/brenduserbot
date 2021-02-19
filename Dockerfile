FROM Brend-Support/brend-userbot:latest
RUN git clone https://github.com/Brend-Support/Brend-UserBot/root/Brend-UserBot
WORKDIR /root/BrendUserBot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
