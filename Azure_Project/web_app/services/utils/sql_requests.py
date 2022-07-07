# SELECTION
CHECK_IF_TAG_EXIST = "SELECT tag FROM tag WHERE tag = %s"
GET_IMAGE_TAGS = "SELECT tag FROM link_image_tags where image_IDBASE = (SELECT IDBASE from image WHERE name = %s)"
GET_IMAGES_BY_TAGS = "SELECT * FROM image where IDBASE in (SELECT image_IDBASE from link_image_tags WHERE tag IN ({}) or name IN ({})) ORDER BY name"
GET_ALL_IMAGES = "SELECT * FROM image ORDER BY name"

# INSERTION
INSERT_NEW_TAG = "INSERT INTO tag(tag) VALUES (%s)"
INSERT_NEW_IMAGE = "INSERT INTO image(name, description, container_name, url) VALUES (%s, %s, %s, %s)"
INSERT_LINK = "INSERT INTO link_image_tags(image_IDBASE, tag) VALUES (%s, %s)"
