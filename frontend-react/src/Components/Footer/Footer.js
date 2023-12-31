import React from "react";
import "./Footer.css";

export default function Footer(props) {
  return (
    <div className="footer">
      <h4>{props.note}</h4>
    </div>
  );
}
