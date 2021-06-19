
# A weather tracking and processing application split into multiple microservices
""" services include:
    Data service for database (todo),
    Registering service that takes data from real world data points,
        ex: weather channel or a large json file of "experimental data"
        This large json file can help us learn how to gzip and send large data files between
        services and having an upload service (todo)
    visual service to map out all the regions as a bitmap/cartesian map (todo)
    Warning system that regularly checks for dangerous regions, this will help us work with rabbit messaging queue and
        producer/consumer microservices (todo)
"""

# The visualization ap does not have to be a webpage,
# it can be a desktop application that takes data from the web service

if __name__ == '__main__':
    print('PyCharm')
