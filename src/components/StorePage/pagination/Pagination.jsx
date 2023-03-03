import React from "react";
import "./pagination.css";
import { FaArrowRight, FaArrowLeft } from "react-icons/fa";
function Pagination({ next, prev, onPrevious, onNext }) {
  const handlePrevius = () => {
    onPrevious();
  };
  const handleNext = () => {
    onNext();
  };
  return (
    <nav className="pagination__container">
      <ul className="pagination__container-items">
        {prev ? (
          <li>
            <button
              className="pagination__container-btn"
              onClick={handlePrevius}
            >
              <FaArrowLeft />
            </button>
          </li>
        ) : null}
        {next ? (
          <li>
            <button className="pagination__container-btn" onClick={handleNext}>
              <FaArrowRight />
            </button>
          </li>
        ) : null}
      </ul>
    </nav>
  );
}

export default Pagination;
