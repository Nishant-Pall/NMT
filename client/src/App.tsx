import React, { Fragment, FC, useState, useEffect } from "react";
import api from "./services/api";

const App: FC = () => {
    const [input, setInput] = useState("");
    const [output, setOutput] = useState("");
    const getTranslation = async () => {
        const translation = await api.post("/predict", {
            input_text: input,
        });
        setOutput(translation.data.predicted_translation);
    };
    useEffect(() => {
        const timer = setTimeout(async () => {
            const translation = await api.post("/predict", {
                input_text: input,
            });
            setOutput(translation.data.predicted_translation);
        }, 1000);
        return () => {
            clearTimeout(timer);
        };
    }, [input]);
    return (
        <Fragment>
            <div className="container">
                <div className="row">
                    <div className="col-lg-4">
                        <div className="input-header">
                            <h4>English text</h4>
                        </div>
                        <div className="text-body">
                            <form>
                                <textarea
                                    value={input}
                                    onChange={(e) => {
                                        setInput(e.target.value);
                                    }}
                                    placeholder="Input english sentence"
                                    className="text-area"
                                    cols={30}
                                    rows={10}
                                ></textarea>
                            </form>
                        </div>
                    </div>
                    <div className="button col-lg-4">
                        <button
                            className="btn btn-primary btn-block translate-button"
                            onClick={getTranslation}
                        >
                            Translate
                        </button>
                    </div>
                    <div className="col-lg-4">
                        <div className="input-header">
                            <h4>Spanish translation</h4>
                        </div>
                        <div className="text-body">
                            <form>
                                <textarea
                                    value={output}
                                    disabled={true}
                                    placeholder="Get translation here"
                                    className="text-area"
                                    cols={30}
                                    rows={10}
                                ></textarea>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </Fragment>
    );
};

export default App;
