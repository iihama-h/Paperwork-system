def isnot_detail_empty(post_data, i, field, empty_value):
    return post_data.get('quotations_details_set-' +
                         str(i) + '-' + field) != empty_value
