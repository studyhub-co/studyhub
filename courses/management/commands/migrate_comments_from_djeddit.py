from django.core.management.base import BaseCommand


def copy_comments(**kwargs):
    if ('_DJThread', '_DJTopic', '_DJPost', '_DJUserPostVote', '_Topic', '_Thread', '_Post', '_UserPostVote') in kwargs:
        DJThread = kwargs['_DJThread']
        DJTopic = kwargs['_DJTopic']
        DJPost = kwargs['_DJPost']
        DJUserPostVote = kwargs['_DJUserPostVote']
        Topic = kwargs['_Topic']
        Thread = kwargs['_Thread']
        Post = kwargs['_Post']
        UserPostVote = kwargs['_UserPostVote']
    else:
        from react_comments_django.models import Topic, Thread, Post, UserPostVote
        from djeddit.models import Topic as DJTopic, Thread as DJThread, Post as DJPost, UserPostVote as DJUserPostVote

    # copy posts
    from django.db import connection
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO react_comments_django_post (content,
        created_on,
        modified_on,
        uid,
        lft,
        rght,
        tree_id,
        level,
        created_by_id,
        parent_id,
        _downvotes,
        _upvotes,
        wsi,
        ip_address,
        user_agent,
        deleted_on) 
SELECT content,
        created_on,
        modified_on,
        uid::"uuid",
        lft,
        rght,
        tree_id,
        level,
        created_by_id,
        parent_id,
        _downvotes,
        _upvotes,
        wsi,
        ip_address,
        user_agent,
        deleted_on
 FROM djeddit_post;""")
    #    cursor.execute("""INSERT INTO react_comments_django_post SELECT * FROM djeddit_post;""")
    # copy topics
    for djtopic in DJTopic.objects.all():
        new_topic = Topic()
        for field in djtopic._meta.get_fields():
            if field.name in ('thread',):
                continue

            new_field_value = getattr(djtopic, field.name)
            setattr(new_topic, field.name, new_field_value)

        new_topic.save()

        # copy threads
        for djthread in djtopic.thread.all():
            new_thread = Thread()

            for field in djthread._meta.get_fields():
                if field.name in (
                        'course_question',
                        'textbook_resource',
                        'textbook_solution',
                        'textbook_problem',
                        'topic',
                        'op'
                ):
                    continue  # course_question already copied in migrate script

                new_field_value = getattr(djthread, field.name)
                setattr(new_thread, field.name, new_field_value)

            # the first op post
            new_thread.op = Post.objects.get(uid=djthread.op.uid)
            new_thread.topic = new_topic
            new_thread.save()

    # update id sequences
    cursor.execute("""SELECT setval('react_comments_django_thread_id_seq', (SELECT MAX(id) FROM react_comments_django_thread));""")
    cursor.execute(
        """SELECT setval('react_comments_django_topic_id_seq', (SELECT MAX(id) FROM react_comments_django_topic));""")
    cursor.execute(
        """SELECT setval('react_comments_django_userpostvote_id_seq', (SELECT MAX(id) FROM react_comments_django_userpostvote));""")


    # copy users votes
    for djvote in DJUserPostVote.objects.all():
        UserPostVote.objects.create(val=djvote.val,
                                               post=Post.objects.get(uid=djvote.post_id),
                                               user=djvote.user)

    # replace djeddit notification for posts
    # replace notification target object
    from notifications.models import Notification
    from django.contrib.contenttypes.models import ContentType
    # action Post
    post_content_type = ContentType.objects.get_for_model(DJPost)
    notifications_action_posts = Notification.objects.filter(action_object_content_type=post_content_type)

    new_post_content_type = ContentType.objects.get_for_model(Post)
    notifications_action_posts.update(action_object_content_type=new_post_content_type)

    # target Thread
    thread_content_type = ContentType.objects.get_for_model(DJThread)
    notifications_target_threads = Notification.objects.filter(target_content_type=thread_content_type)

    new_thread_content_type = ContentType.objects.get_for_model(Thread)
    notifications_target_threads.update(target_content_type=new_thread_content_type)


class Command(BaseCommand):
    help = 'migrate comments from djeddit to react-comments-django'

    def handle(self, *args, **options):
        # FYI clear tables:
        # TRUNCATE TABLE react_comments_django_post CASCADE;
        # TRUNCATE TABLE react_comments_django_topic CASCADE;
        # TRUNCATE TABLE react_comments_django_userpostvote;
        copy_comments()



