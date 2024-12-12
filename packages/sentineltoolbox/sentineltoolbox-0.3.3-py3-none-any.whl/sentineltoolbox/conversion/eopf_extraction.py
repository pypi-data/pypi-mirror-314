import logging

logger = logging.getLogger("sentineltoolbox.conversion")


def extract_metatadata_with_eopf(upath):
    attrs = {}
    try:
        from eopf.store.safe import EOSafeStore
    except ImportError:
        logger.warning("You need to install EOPF to support root metadata extraction else metadata will be empty")
    else:
        try:
            store = EOSafeStore(upath.url, storage_options=upath.fs.storage_options).open()
            eoproduct = store.load(metadata_only=True)
            attrs = eoproduct.attrs
        except Exception as e:
            logger.exception(e)
    return attrs
