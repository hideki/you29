import logging;
from django import template
register = template.Library();

@register.filter("truncate_chars")
def truncate_chars(value, max_length):
    logging.debug("value="+value + " max_length="+str(max_length));
    if len(value) > max_length:
        logging.debug("len="+str(len(value)));
        truncd_val = value[:max_length:]
        #if value[max_length+1] != " ":
        #    truncd_val = truncd_val[:truncd_val.rfind(" ")]
        return  truncd_val + "..."
    return value
