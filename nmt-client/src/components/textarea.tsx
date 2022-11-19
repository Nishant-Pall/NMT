import React, { Fragment, FC } from "react";
type Props = {
    value: string;
    placeholder: string;
    disabled: boolean;
    rows: number;
    cols: number;
    className: string;
    onChange?: (params: string) => void;
};

const Textarea: FC<Props> = (props: Props) => {
    const { disabled, value, onChange, className, rows, cols, placeholder } =
        props;
    return (
        <Fragment>
            <form>
                <textarea
                    value={value}
                    onChange={(e) => {
                        onChange?.(e.target.value);
                    }}
                    disabled={disabled}
                    placeholder={placeholder}
                    className={className}
                    cols={cols}
                    rows={rows}
                ></textarea>
            </form>
        </Fragment>
    );
};

export default Textarea;
