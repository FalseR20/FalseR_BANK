import React, {Component} from 'react';
import {createRoot} from "react-dom/client";

class AppHome extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            loaded: false,
            placeholder: "Loading"
        };
    }

    componentDidMount() {
        fetch("/api/cards")
            .then(response => {
                if (response.status > 400) {
                    return this.setState(() => {
                        return {placeholder: "Something went wrong!"};
                    });
                }
                return response.json();
            })
            .then(data => {
                this.setState(() => {
                    return {
                        data,
                        loaded: true
                    };
                });
            });
    }

    render() {
        let dateNow = new Date();
        return (
            <div className="cards-panel">{this.state.data.map(card => {
                let expiration_date = new Date(card.expiration_date);
                return (
                    <a className="card-block grid but"
                       href={`/cards/${card.number}`}
                       style={
                           expiration_date < dateNow
                               ? {borderColor: "orangered"}
                               : card.is_freeze === true
                                   ? {borderColor: "dodgerblue"}
                                   : {borderColor: ""}
                       }
                       key={`card_${card.number}`}>
                        <div style={{gridArea: "number"}}>{card.number}</div>
                        <div style={{gridArea: "name"}}>{card.cardholder_name}</div>
                        <div style={{
                            gridArea: "date",
                            textAlign: "right"
                        }}>{`${expiration_date.getMonth() + 1}/${expiration_date.getFullYear() % 100}`}</div>
                        <div style={{
                            gridArea: "balance",
                            textAlign: "center"
                        }}>{parseFloat(card.account.balance).toFixed(2)} {card.account.currency.code}</div>
                    </a>
                );
            })}
                <a className="card-block but new" href="/cards/new/">+</a>
            </div>
        );
    }
}

export default AppHome;

const container = document.getElementById("app-home");
const root = createRoot(container);
root.render(<AppHome/>);