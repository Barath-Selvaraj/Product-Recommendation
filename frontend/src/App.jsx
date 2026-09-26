import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [limit, setLimit] = useState(5);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!query.trim()) {
      return;
    }
    const userQuery = query.trim();

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        type: "user",
        text: userQuery,
      },
    ]);
    setQuery("");
    setLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8000/recommendations/?query=${encodeURIComponent(
          query
        )}&limit=${limit}`
      );

      const data = await response.json();

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          type: "bot",
          products: data,
        },
      ]);

      setProducts(data);
    } catch (error) {
      console.error("API error:", error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="app">
      <header className="header">
        <h1>AI Product Search</h1>
        <p>Find products using semantic search</p>
      </header>

      <main className="main-content">
        <div className="chat">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.type}`}
            >
              {message.type === "user" ? (
                message.text
              ) : (
                <div className="bot-response">
                  <div className="bot-label">AI Product Search</div>

                  <div className="bot-products">
                  </div>
                  {message.products.map((product) => (
                    <div
                      className="product-card"
                      key={product.product_id}
                    >
                      <h2>{product.product_title}</h2>

                      <p>
                        <strong>Brand:</strong>{" "}
                        {product.product_brand || "N/A"}
                      </p>

                      <p>
                        <strong>Color:</strong>{" "}
                        {product.product_color || "N/A"}
                      </p>

                      <p>
                        <strong>Similarity:</strong>{" "}
                        {product.similarity_score.toFixed(3)}
                      </p>

                      <p>
                        <strong>ESCI:</strong>{" "}
                        {product.esci_label}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
        <div className="search-area">
          <form onSubmit={handleSubmit} className="search-form">
            <input
              type="text"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search for a product..."
            />

            <button type="submit" disabled={loading}>
              {loading ? "Searching..." : "Send"}
            </button>
          </form>

          <div className="limit-control">
            <label htmlFor="limit">
              Recommendations:
            </label>

            <select
              id="limit"
              value={limit}
              onChange={(event) =>
                setLimit(Number(event.target.value))
              }
            >
              <option value={1}>1</option>
              <option value={2}>2</option>
              <option value={3}>3</option>
              <option value={4}>4</option>
              <option value={5}>5</option>
            </select>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;