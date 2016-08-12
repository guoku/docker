FROM gkspider_base:latest
MAINTAINER anchen@guoku.com


COPY . /usr/app/
ENV PYTHONPATH /usr/app:/usr/app/entity_spider/api
ENV C_FORCE_ROOT 1

ENTRYPOINT ["/usr/app/entry.sh"]
CMD ["/bin/bash"]