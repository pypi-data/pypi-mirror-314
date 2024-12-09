FROM python:3

WORKDIR /var/lib/dsh-server

RUN mkdir -p /var/lib/dsh-server
RUN mkdir -p /var/lib/dsh-server/data
RUN mkdir -p /var/lib/dsh-server/posts
RUN mkdir -p /var/lib/dsh-server/uploader

RUN pip install dataset.sh['all']
RUN pip install gunicorn

ENV DATASET_APP_STORAGE_LOCATION=/var/lib/dsh-server/data
ENV DATASET_APP_ARTICLE_LOCATION=/var/lib/dsh-server/posts
ENV DATASET_APP_UPLOADER_DIR=/var/lib/dsh-server/uploader
ENV DATASET_SH_SERVER_CONFIG_FILE=/var/lib/dsh-server/dataset-sh-server-config.json
ENV SERVER_NAME=localhost:8989

RUN dataset-sh-server config init

CMD ["gunicorn"  , "-b", "0.0.0.0:8989", "dataset_sh.server.app:create_app()"]
