
#model snippets


class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

    when creating, it becomes shirt_size = "(one of options)"


    '''
    On user object, inforce unique=True on email. 
        
        need to find a way to properly handle errors.


        models.ForeignKey('self')



   Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name (db_table), or human-readable singular and plural names (verbose_name and verbose_name_plural). None are required, and adding class Meta to a model is completely optional. 


    model methods cannot be used on object instances. use model definitions for that.

    '''


