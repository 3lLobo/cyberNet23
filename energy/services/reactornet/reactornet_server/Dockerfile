FROM php:8-apache
RUN apt-get update && apt-get install --no-install-recommends -y openssh-server sudo libpq-dev cron
RUN docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql && docker-php-ext-install pgsql pdo_pgsql
RUN sed -i -e  's/Listen 80/Listen 127.0.0.1:80/' /etc/apache2/ports.conf
RUN useradd -r -d /data/home/remote -s /bin/bash -u 5082 remote && \
        echo "remote ALL=(nobody) NOPASSWD: /bin/reactornet_browser" > /etc/sudoers.d/remote && \
        chmod 0440 /etc/sudoers.d/remote
COPY start.sh /start.sh
COPY ssh/* /etc/ssh/
COPY www/ /var/www/html/
COPY etc/php.ini /usr/local/etc/php
COPY bin/autoremove /bin/autoremove
COPY bin/reactornet_browser /bin/reactornet_browser
RUN mkdir -p /var/www/html/files
RUN chown www-data:www-data /var/www/html/files
RUN chown root:root /var/www/html
RUN chmod 755 /var/www/html
RUN echo "*/15 * * * * /bin/autoremove" | crontab -u www-data -
RUN chmod 600 /etc/ssh/ssh_*
CMD ["/start.sh"]
