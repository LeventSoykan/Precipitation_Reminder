FROM ubuntu

# Install python, pip and cron
RUN apt-get update 
RUN apt-get install -y python3 python3-pip
RUN apt-get -y install cron

# Create app directory
RUN mkdir /app/

# Install packages
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy python script
COPY precip.py /app/precip.py

# Copy daily cron file to the cron.d directory
COPY daily_cron /etc/cron.d/daily_cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/daily_cron 

# Apply cron job
RUN crontab /etc/cron.d/daily_cron
 
# Run the command on container startup
CMD  ["/bin/bash", "-c", "printenv > /etc/environment && cron -f"]
