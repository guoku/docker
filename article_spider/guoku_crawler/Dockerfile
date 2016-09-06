FROM gk_article_base:latest

COPY . /usr/app/
RUN pip install -e .

ENTRYPOINT ["/usr/app/entry.sh"]
CMD ["/bin/bash"]
