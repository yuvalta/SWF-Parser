import matplotlib.pyplot as plt


def plot_users_dict(dictionary):
    for user in dictionary:
        plt.bar(user, dictionary[user][1])

    plt.xlabel('User ID')
    plt.xticks(rotation=90)
    plt.ylabel('# of occurrences')
    plt.title('How many time\neach user used the system')

    plt.show()


def plot_jobs_dict(dictionary):
    plt.bar(list(dictionary.keys()), list(dictionary.values()))
    plt.xticks(range(len(dictionary)), list(dictionary.keys()))

    plt.xlabel('Job size')
    plt.ylabel('# of occurrences')
    plt.title('Jobs sizes')

    plt.show()
