from flextables import getFlextables
fp = open("dummy","w")
getFlextables("generation-results",fp)
fp.close()
