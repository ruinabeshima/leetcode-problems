class Twitter:

    def __init__(self):
        self.following = defaultdict(set)
        self.posts = defaultdict(list)
        self.count = 0 

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.posts[userId].append((self.count, tweetId))
        self.count -= 1 

    def getNewsFeed(self, userId: int) -> list[int]:
        heap = []
        for user in self.following[userId] | {userId}: 
            for count, postId in self.posts[user]: 
                heapq.heappush(heap, (count, postId))

        feed = []
        while len(heap) > 0 and len(feed) < 10: 
            count, postId = heapq.heappop(heap)
            feed.append(postId)

        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)
        


# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)
