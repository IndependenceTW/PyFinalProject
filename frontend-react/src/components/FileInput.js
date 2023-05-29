import { useState, useEffect } from "react";
import Button from "@material-ui/core/Button";
import Box from "@material-ui/core/Box";
import Cookies from "universal-cookie";
import Iconify from "./Iconify";

const FileInput = (setForm) => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const cookies = new Cookies();

    useEffect(() => {
        if (selectedImage) {
            setImageUrl(URL.createObjectURL(selectedImage));
            var formData = new FormData();
            formData.append("image", selectedImage, selectedImage.name);
            setForm.setForm(formData);
        }
    }, [selectedImage]);

    


    return (
        <>
            <input
                accept="image/*"
                type="file"
                id="select-image"
                style={{ display: "none" }}
                onChange={(e) => setSelectedImage(e.target.files[0])}
            />
            <label htmlFor="select-image">
                <Button variant="contained" color="primary" component="span" startIcon={<Iconify icon="material-symbols:add-photo-alternate-outline"/>}>
                    Upload Image
                </Button>
            </label>
            {imageUrl && selectedImage && (
                <Box mt={2} textAlign="center">
                    <div>Image Preview:</div>
                    <img src={imageUrl} alt={selectedImage.name} height="100px" />
                </Box>
            )}
        </>
    );
};

export default FileInput;