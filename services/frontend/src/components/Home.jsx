import React from "react";

const Home = () => (
  <div>
    <section className="hero is-fullheight is-default is-bold">
      <div className="hero-body">
        <div className="container">
          <div className="columns is-vcentered">
            <div className="column is-5 is-offset-1 landing-caption">
              <h1 className="title is-1 is-bold is-spaced">
                Meet FRED
              </h1>
              <h2 className="subtitle is-5 is-muted">
                Dig's An End-to-End Boilerplate for Full Stack Development
              </h2>
            </div>
            <div className="column is-5">
              <figure className="image is-4by3">
                <a href="https://undraw.co/">
                  <img
                    src={
                      process.env.PUBLIC_URL + "/img/illustrations/designer.svg"
                    }
                    alt="fred at work"
                  />
                </a>
              </figure>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
);

export default Home;
