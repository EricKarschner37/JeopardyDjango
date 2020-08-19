var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ClueSquare = function (_React$Component) {
  _inherits(ClueSquare, _React$Component);

  function ClueSquare(props) {
    _classCallCheck(this, ClueSquare);

    var _this = _possibleConstructorReturn(this, (ClueSquare.__proto__ || Object.getPrototypeOf(ClueSquare)).call(this, props));

    _this.state = { hasBeenClicked: false };
    _this.handleClick = _this.handleClick.bind(_this);
    return _this;
  }

  _createClass(ClueSquare, [{
    key: "handleClick",
    value: function handleClick(e) {
      if (!this.state.hasBeenClicked) {
        this.setState({ 'hasBeenClicked': true });
        this.props.onClueSquareClick(this.props.row, this.props.col);
      }
    }
  }, {
    key: "render",
    value: function render() {
      return React.createElement(
        "td",
        { className: "clue", onClick: this.handleClick },
        !this.state.hasBeenClicked && React.createElement(
          "p",
          { className: "cost" },
          this.props.cost
        )
      );
    }
  }]);

  return ClueSquare;
}(React.Component);

var ClueBoard = function (_React$Component2) {
  _inherits(ClueBoard, _React$Component2);

  function ClueBoard(props) {
    _classCallCheck(this, ClueBoard);

    var _this2 = _possibleConstructorReturn(this, (ClueBoard.__proto__ || Object.getPrototypeOf(ClueBoard)).call(this, props));

    _this2.getCostForRow = _this2.getCostForRow.bind(_this2);
    return _this2;
  }

  _createClass(ClueBoard, [{
    key: "handleClueSquareClick",
    value: function handleClueSquareClick(row, col) {
      revealClue(row, col);
      console.log("Clicked: " + row + " " + col);
    }
  }, {
    key: "getCostForRow",
    value: function getCostForRow(row) {
      return (row + 1) * 200;
    }
  }, {
    key: "render",
    value: function render() {
      var categorySquares = [];
      this.props.categories.map(function (category, key) {
        console.log(category + ": " + key);
        categorySquares.push(React.createElement(
          "th",
          { key: key, className: "category" },
          React.createElement(
            "p",
            null,
            category
          )
        ));
      });
      console.log(this.props.categories);
      console.log(categorySquares);

      var clueRows = [];
      for (var i = 0; i < 5; i++) {
        var clues = [];
        for (var j = 0; j < 6; j++) {
          clues.push(React.createElement(ClueSquare, { cost: this.getCostForRow(i), onClueSquareClick: this.handleClueSquareClick, row: i, col: j, hasBeenClicked: false }));
        }
        clueRows.push(React.createElement(
          "tr",
          null,
          clues
        ));
      }

      return React.createElement(
        "table",
        { id: "clue_table" },
        React.createElement(
          "tbody",
          null,
          React.createElement(
            "tr",
            null,
            categorySquares
          ),
          clueRows
        )
      );
    }
  }]);

  return ClueBoard;
}(React.Component);