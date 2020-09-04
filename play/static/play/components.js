var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var BuzzerButton = function (_React$Component) {
    _inherits(BuzzerButton, _React$Component);

    function BuzzerButton(props) {
        _classCallCheck(this, BuzzerButton);

        var _this = _possibleConstructorReturn(this, (BuzzerButton.__proto__ || Object.getPrototypeOf(BuzzerButton)).call(this, props));

        _this.handleClick = _this.handleClick.bind(_this);
        return _this;
    }

    _createClass(BuzzerButton, [{
        key: "handleClick",
        value: function handleClick(e) {
            e.preventDefault();
            this.props.onBuzz();
        }
    }, {
        key: "render",
        value: function render() {
            return React.createElement(
                "button",
                { className: "buzzer", onClick: this.handleClick },
                "BUZZ"
            );
        }
    }]);

    return BuzzerButton;
}(React.Component);

var ClueDisplay = function (_React$Component2) {
    _inherits(ClueDisplay, _React$Component2);

    function ClueDisplay(props) {
        _classCallCheck(this, ClueDisplay);

        return _possibleConstructorReturn(this, (ClueDisplay.__proto__ || Object.getPrototypeOf(ClueDisplay)).call(this, props));
    }

    _createClass(ClueDisplay, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "p",
                    { className: "cost" },
                    this.props.cost
                ),
                React.createElement(
                    "p",
                    { className: "clue" },
                    this.props.clue
                ),
                React.createElement(
                    "p",
                    { className: "answer" },
                    this.props.answer
                )
            );
        }
    }]);

    return ClueDisplay;
}(React.Component);

var UserInformation = function (_React$Component3) {
    _inherits(UserInformation, _React$Component3);

    function UserInformation(props) {
        _classCallCheck(this, UserInformation);

        return _possibleConstructorReturn(this, (UserInformation.__proto__ || Object.getPrototypeOf(UserInformation)).call(this, props));
    }

    _createClass(UserInformation, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "p",
                { className: "name" },
                this.props.name
            );
        }
    }]);

    return UserInformation;
}(React.Component);

var BuzzerDisplay = function (_React$Component4) {
    _inherits(BuzzerDisplay, _React$Component4);

    function BuzzerDisplay(props) {
        _classCallCheck(this, BuzzerDisplay);

        return _possibleConstructorReturn(this, (BuzzerDisplay.__proto__ || Object.getPrototypeOf(BuzzerDisplay)).call(this, props));
    }

    _createClass(BuzzerDisplay, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                null,
                React.createElement(UserInformation, { name: this.props.name }),
                React.createElement(ClueDisplay, { clue: this.props.question, answer: this.props.answer, cost: this.props.cost }),
                this.props.buzzed && React.createElement(
                    "p",
                    null,
                    "You are buzzed in"
                ),
                React.createElement(BuzzerButton, { onBuzz: this.props.onBuzz })
            );
        }
    }]);

    return BuzzerDisplay;
}(React.Component);