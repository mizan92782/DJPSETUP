import uuid

def ProfileImagePath(instance, filename):
    ext = filename.split('.')[-1]
    return f"practitioner_dp/{uuid.uuid4()}.{ext}"
