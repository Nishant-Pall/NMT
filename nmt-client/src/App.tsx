import React, {
    Fragment,
    FC,
    useState,
    useEffect,
    useCallback,
    useRef,
} from "react";
import Textarea from "./components/textarea";
import api from "./services/api";

const App: FC = () => {
    const [input, setInput] = useState("");
    let outputRef = useRef("");

    const requestTranslation = useCallback(async () => {
        const translation = await api.post("/predict", {
            input_text: input,
        });
        outputRef.current = translation.data.predicted_translation;
    }, [input]);

    const getTranslation = async () => {
        requestTranslation();
    };

    useEffect(() => {
        if (input) {
            const timer = setTimeout(() => {
                requestTranslation();
            }, 1000);
            return () => {
                clearTimeout(timer);
            };
        }
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
                                value={outputRef.current}
                                disabled={true}
                                placeholder="Get translation here"
                                className="text-area"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </Fragment>
    );
};

export default App;
