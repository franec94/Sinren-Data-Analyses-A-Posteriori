CREATE TABLE "compressions" (
	"width"	INTEGER NOT NULL CHECK("width" > 0),
	"height"	INTEGER NOT NULL CHECK("height" > 0),
	"crop_width"	INTEGER NOT NULL CHECK("crop_width" > 0),
	"crop_heigth"	INTEGER NOT NULL CHECK("crop_heigth" > 0),
	"image"	TEXT NOT NULL,
	"quality"	INTEGER NOT NULL CHECK("quality" > 0 AND "quality" < 100),
	"bpp"	REAL CHECK("bpp" > 0),
	"mse_score"	REAL CHECK("mse_score" >= 0),
	"psnr_score"	REAL CHECK("psnr_score" >= 0),
	"ssim_score"	REAL,
	"cr_score"	REAL CHECK("cr_score" > 0),
	"is_cropped"	BLOB NOT NULL CHECK("is_cropped" = true OR "is_cropped" = false),
	PRIMARY KEY("crop_width","crop_heigth","image","quality")
)