SELECT ct.quality, COUNT(*) AS tot,
	AVG(ct.bpp) AS avg_bpp,
	AVG(ct.mse_score) AS avg_mse,
	AVG(ct.psnr_score) AS avg_psnr,
	AVG(ct.ssim_score) AS avg_ssim,
	AVG(ct.cr_score) AS avg_cr
FROM compressions_table AS ct
WHERE ct.crop_width = 256 AND ct.crop_heigth = 256
GROUP BY  ct.quality;

SELECT ct.image, COUNT(*) AS tot,
	AVG(ct.bpp) AS avg_bpp,
	AVG(ct.mse_score) AS avg_mse,
	AVG(ct.psnr_score) AS avg_psnr,
	AVG(ct.ssim_score) AS avg_ssim,
	AVG(ct.cr_score) AS avg_cr
FROM compressions_table AS ct
WHERE ct.crop_width = 256 AND ct.crop_heigth = 256
GROUP BY ct.image
ORDER BY ct.image;
