
def Iou(inputs,targets,thresholds=[0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80]):
    ts_sum = 0
    for i in range(len(thresholds)):
        inputs_copy = inputs.flatten().copy()   # nputs_copy = inputs.flatten().clone()
        targets_copy = targets.flatten().copy()
        inputs_copy[inputs.flatten() < thresholds[i]] = 0
        inputs_copy[inputs.flatten() >= thresholds[i]] = 1
        targets_copy[targets.flatten() < thresholds[i]] = 0
        targets_copy[targets.flatten() >= thresholds[i]] = 1
        intersection = (inputs_copy.flatten() * targets_copy).sum()
        total = (inputs_copy.flatten() + targets_copy).sum()
        union = total - intersection
        iou = (intersection + 1e-16)/ (union + 1e-16)
        ts_sum += iou
    return ts_sum/len(thresholds)

def IouOrder(inputs,targets,thresholds=[15]):
    lower_threshold = thresholds[0]
    upper_threshold = thresholds[1]
    inputs_copy = (inputs.flatten() >= lower_threshold) & (inputs.flatten() <= upper_threshold)
    targets_copy = (targets.flatten() >= lower_threshold) & (targets.flatten() <= upper_threshold)
    inputs_copy = inputs_copy.astype(int)
    targets_copy = targets_copy.astype(int)
    intersection = (inputs_copy.flatten() * targets_copy).sum()
    total = (inputs_copy.flatten() + targets_copy).sum()
    union = total - intersection
    iou = (intersection + 1e-16)/ (union + 1e-16)
    return iou

 