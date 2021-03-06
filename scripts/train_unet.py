"""
script is used for instatiate a U-Net model and trains with given images in a directory.

"""
import os
from img_segmentation.model import UNet

# for apple
# file_base = '/Users/simonkramer/Documents/Polybox/4.Semester/Master_Thesis/03_ImageSegmentation/structure_vidFloodExt/'

# for windows
tune_vid = ''
file_base = 'C:\\Users\\kramersi\\polybox\\4.Semester\\Master_Thesis\\03_ImageSegmentation\\structure_vidFloodExt\\'
model_names = ['train_test_l5_refaug', 'train_test_l5_aug_reduced', 'train_test_l5_']
aug = [False, False, False]
feat = [16, 16, 16, 32, 16, 8]
ep = [200, 200, 200, 200, 200, 200]
lay = [5, 5, 5, 4, 5, 6]
drop = [0.75, 0.75, 0.75, 0.75, 0.75, 0.75]
bat = [2, 2, 2, 4, 8, 6]
res = [True, True, True, False, False, False]
bd = [None, None, None, None, None, None]  # os.path.join(file_base, 'models', 'train_test_l5_' + tune_vid + 'Top')
# bd = [os.path.join(file_base, 'models', 'ft_l5b3e200f16_dr075i2res_lr'), None, None]

rois = {
    'AthleticPark': [102, 171, 327, 236],
    'FloodXCam1': [275, 136, 174, 62],
    'FloodXCam5': [8, 239, 101, 43],
    'HoustonGarage': [185, 114, 205, 217],
    'HarveyParking': [127, 267, 95, 105],
    'BayouBridge': [58, 124, 401, 259]
}

for i, model_name in enumerate(model_names):
    if i in [0, 1, 2]:
        #model_dir = os.path.join(file_base, 'models', model_name)

        #if not os.path.isdir(model_dir):
            #os.mkdir(model_dir)

        # configs for fine tune
        # base_model_dir = os.path.join(file_base, 'models', 'cflood_c2l5b3e40f16_dr075caugi2res')
        # base_model_dir = os.path.join(file_base, 'models', 'cflood_c2l4b3e60f64_dr075caugi2')
        #
        # train_dir_ft = os.path.join(file_base, 'video_masks', 'CombParkGarage_train')
        # valid_dir_ft = os.path.join(file_base, 'video_masks', 'CombParkGarage_validate')
        # pred_dir_ft = os.path.join(file_base, 'models', model_name, 'test_img_tf')
        # if not os.path.isdir(pred_dir_ft):
        #     os.mkdir(pred_dir_ft)

        # # configs for training from scratch
        train_dir_flood = 'E:\\watson_for_trend\\3_select_for_labelling\\dataset__flood_2class\\train' # os.path.join(file_base, 'video_masks', 'floodX_cam1', 'train')
        valid_dir_flood = 'E:\\watson_for_trend\\3_select_for_labelling\\dataset__flood_2class\\validate'  #os.path.join(file_base, 'video_masks', 'floodX_cam1', 'validate')
        test_dir_flood = 'E:\\watson_for_trend\\3_select_for_labelling\\dataset__flood_2class\\test'  #os.path.join(file_base, 'video_masks', 'floodX_cam1', 'validate')

        # paths for finetune
        train_dir_further = os.path.join(file_base, 'other_video_masks', 'FurtherYoutube', 'train')
        valid_dir_further = os.path.join(file_base, 'other_video_masks', 'FurtherYoutube', 'validate')

        train_tune_dir = os.path.join(file_base, 'video_masks', tune_vid, 'train')
        valid_tune_dir = os.path.join(file_base, 'video_masks', tune_vid, 'validate')

        pred_dir_flood = os.path.join(file_base, 'models', model_name, 'test_img')
        if not os.path.isdir(pred_dir_flood):
            os.mkdir(pred_dir_flood)

        # configs for testing model
        test_dir_elliot = os.path.join(file_base, 'frames', 'elliotCityFlood')
        test_dir_athletic = os.path.join(file_base, 'frames', 'ChaskaAthleticPark')
        test_dir_floodx = os.path.join(file_base, 'frames', 'FloodX')

        #pred_dir = os.path.join(file_base, 'predictions', model_name)
        #if not os.path.isdir(pred_dir):
            #os.mkdir(pred_dir)

        test_dir = os.path.join(file_base, 'video_masks', '*')

        img_shape = (512, 512, 3)
        unet = UNet(img_shape, root_features=feat[i], layers=lay[i], batch_norm=True, dropout=drop[i], inc_rate=2., residual=res[i])

        #unet.train(model_dir, [train_dir_flood, train_dir_further], [valid_dir_flood, valid_dir_further], batch_size=bat[i], epochs=ep[i], augmentation=aug[i], base_dir=bd[i], save_aug=False, learning_rate=0.001)
        # unet.test(model_dir, [test_dir_flood], pred_dir_flood)
        #test_dir = os.path.join(file_base, 'video_masks', '*')
        #
        import glob
        for test in glob.glob(test_dir):  # test for all frames in directory
            base, tail = os.path.split(test)
            if i in [0, 1]:
                model_dir = os.path.join(file_base, 'models', model_name)
            else:
                model_dir = os.path.join(file_base, 'models', model_name + tail)
            pred = os.path.join(model_dir, 'pred_roi_' + tail)
            csv_path = os.path.join(model_dir, tail + '_roi.csv')
            test_val = os.path.join(test, 'validate')
            if not os.path.isdir(pred):
                os.mkdir(pred)



            unet.test(model_dir, [test_val], pred, csv_path=csv_path, roi=rois[tail])

        # script for storing prediction
        # from keras_utils import overlay_img_mask
        # vid_name = 'FloodXCam1'
        # img_path = os.path.join(file_base, 'video_masks', vid_name, 'validate', 'images')
        # msk_path = os.path.join(file_base, 'video_masks', vid_name, 'validate', 'masks')
        # output = os.path.join(file_base, 'video_masks', vid_name, 'validate', 'human_masks')
        # if not os.path.isdir(output):
        #     os.mkdir(output)
        # im = load_images(img_path)
        # msk = load_masks(msk_path)
        # for nr, (i, m) in enumerate(zip(im, msk)):
        #     name = 'human' + str(nr) + '.png'
        #     overlay_img_mask(m, i, os.path.join(output, name))