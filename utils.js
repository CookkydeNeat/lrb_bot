// Account.js
exports.Account = class Account {
    
    constructor(name) {
        this.name = name;
        this.lastPost = "";
    }
}

exports.Listener = class Listener {
    /**
     * Represent a listener, to keep track of the data
     * @param {number} id 
     * @param {number} frequency 
     */
    constructor(id,frequency) {
        this.id = id
        this.lastFetch = Date.now()
        this.frequency = frequency
    }
    updateLastFetch(){
        this.lastFetch = Date.now()
    }
    theoreticalTimeUntilNextFetch(){
        let period = (this.lastFetch + this.frequency)/1000
        period = Math.trunc(period)
        return `<t:${period}:R>`
    }
}