from datetime import datetime


def uploaded_at(upload_time: datetime):
    td = datetime.now() - upload_time

    print(td)

    up_at = ""
    if td.days >= 365:
        up_at = td.days // 365

        if up_at == 1:
            return f"{up_at} year ago"
        else:
            return f"{up_at} years ago"

    elif td.days >= 30:
        up_at = td.days // 30

        if up_at == 1:
            return f"{up_at} month ago"
        else:
            return f"{up_at} months ago"

    elif td.days >= 1:
        up_at = td.days

        if up_at == 1:
            return f"{up_at} day ago"
        else:
            return f"{up_at} days ago"

    elif td.seconds >= 60 * 60:
        up_at = td.seconds // (60 * 60)

        if up_at == 1:
            return f"{up_at} hour ago"
        else:
            return f"{up_at} hours ago"

    elif td.seconds >= 60:
        up_at = td.seconds // 60

        if up_at == 1:
            return f"{up_at} minute ago"
        else:
            return f"{up_at} minutes ago"

    elif td.seconds >= 1:
        up_at = td.seconds

        if up_at == 1:
            return f"{up_at} second ago"
        else:
            return f"{up_at} seconds ago"

    else:
        return "now"