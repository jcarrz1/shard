from apiclient import errors
# ...

def print_timeline_item_metadata(service, timeline_id):
  """Print some timeline item metadata information.

  Args:
    service: Authorized Mirror service.
    item_id: ID of the timeline item to print metadata information for.
  """
  try:
    timeline_item = service.timeline().get(id=item_id).execute()

    print 'Timeline item ID:  %s' % timeline_item.get('id')
    if timeline_item.get('isDeleted'):
      print 'Timeline item has been deleted'
    else:
      creator = timeline_item.get('creator')
      if creator:
        print 'Timeline item created by  %s' % creator.get('displayName')
      print 'Timeline item created on  %s' % timeline_item.get('created')
      print 'Timeline item displayed on %s' % timeline_item.get('displayTime')
      in_reply_to = timeline_item.get('inReplyTo')
      if in_reply_to:
        print 'Timeline item is a reply to  %s' % in_reply_to
      text = timeline_item.get('text')
      if text:
        print 'Timeline item has text:  %s' % text
      for contact in timeline_item.get('recipients', []):
        print 'Timeline item is shared with:  %s' % contact.get('id')
      notification = timeline_item.get('notification')
      if notification:
        print 'Notification delivery time: %s' % (
            notification.get('deliveryTime'))
        print 'Notification level:  %s' % notification.get('level')
      # See mirror.timeline.attachments.get to learn how to download the
      # attachment's content.
      for attachment in timeline_item.get('attachments', []):      
        print 'Attachment ID: %s' % attachment.get('id')
        print '  > Content-Type: %s' % attachment.get('contentType') 
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


#########################################################################

def print_attachment_metadata(service, item_id, attachment_id):
  """Print an attachment's metadata

  Args:
    service: Authorized Mirror service.
    item_id: ID of the timeline item the attachment belongs to.
    attachment_id: ID of the attachment to print metadata for.
  """
  try:
    attachment = service.timeline().attachments().get(
        itemId=item_id, attachmentId=attachment_id).execute()
    print 'Attachment content type: %s' % attachment['contentType']
    print 'Attachment content URL: %s' % attachment['contentUrl']
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def download_attachment(service, attachment):
  """Download an attachment's content

  Args:
    service: Authorized Mirror service.
    attachment: Attachment's metadata.
  Returns:
    Attachment's content if successful, None otherwise.
  """
  resp, content = service._http.request(attachment['contentUrl'])
  if resp.status == 200:
    return content
  else:
    print 'An error occurred: %s' % resp
    return None

