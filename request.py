class Request:
    rType = None
    paymentMethod = None
    rate = None
    lowerBound = None
    upperBound = None

    def setData(self, *args):
        print(args)
        self.rType = args[1]
        self.paymentMethod = args[3]
        self.rate = args[2]
        self.lowerBound = args[4]
        self.upperBound = args[5]
