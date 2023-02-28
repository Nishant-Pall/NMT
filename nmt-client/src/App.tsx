import React, { Fragment, FC, useState, useEffect, useCallback } from "react";
import Textarea from "./components/textarea";
import api from "./services/api";

const App: FC = () => {
    const [input, setInput] = useState("");
    const [output, setOutput] = useState("");

    const requestTranslation = useCallback(async () => {
        const translation = await api.post("/predict", {
            input_text: input,
        });
        setOutput(translation.data.predicted_translation);
    }, [input]);

    const getTranslation = async () => {
        requestTranslation();
    };

    useEffect(() => {
        const timer = setTimeout(async () => {
            requestTranslation();
        }, 1000);
        return () => {
            clearTimeout(timer);
        };
    }, [input, requestTranslation]);

    return (
        <Fragment>
            <div className="container">
                <div className="row">
                    <div className="col-lg-4">
                        <div className="input-header">
                            <h4>English text</h4>
                        </div>
                        <div className="text-body">
                            <Textarea
                                value={input}
                                onChange={(e) => {
                                    setInput(e);
                                }}
                                disabled={false}
                                placeholder="Input english sentence"
                                className="text-area"
                                cols={30}
                                rows={10}
                            />
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
                            <Textarea
                                value={output}
                                disabled={true}
                                placeholder="Get translation here"
                                className="text-area"
                                cols={30}
                                rows={10}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </Fragment>
    );
};

export default App;
