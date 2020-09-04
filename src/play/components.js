class BuzzerButton extends React.Component {
    constructor(props) {
        super(props);

        this.handleClick = this.handleClick.bind(this)
    }

    handleClick(e) {
        e.preventDefault();
        this.props.onBuzz()
    }

    render() {
        return (
            <button className="buzzer" onClick={this.handleClick}>BUZZ</button>
        )
    }
}

class WagerDisplay extends React.Component {
    constructor(props) {
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this)
    }

    isValidWager(wager){
        return !isNaN(wager) && parseInt(num) >= 5
    }

    handleSubmit(e) {
        e.preventDefault();
        let wager = $("#wager_input").value
        if (this.isValidWager(wager))
        this.props.onWager(parseInt(wager))
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <input type="text" placeholder="Wager" id="wager_input" />
                <input type="submit" value="Wager" />
            </form>
        )
    }
}

class ClueDisplay extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div>
                <p className="cost">{this.props.cost}</p>
                <p className="clue">{this.props.clue}</p>
                <p className="answer">{this.props.answer}</p>
            </div>
        )
    }
}

class UserInformation extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <p className="name">{this.props.name}</p>
        )
    }
}

class BuzzerDisplay extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <UserInformation name={this.props.name}/>
                <ClueDisplay clue={this.props.question} answer={this.props.answer} cost={this.props.cost} />
                {this.props.buzzed && <p>You are buzzed in</p>}
                {this.props.daily_double && <WagerDisplay onWager={this.props.onWager} />}
                {!this.props.daily_double && <BuzzerButton onBuzz={this.props.onBuzz}/>}
            </div>
        )
    }
}