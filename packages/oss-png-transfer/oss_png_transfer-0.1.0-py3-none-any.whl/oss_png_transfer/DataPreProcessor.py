import random
class DataPreProcessor:
    """데이터 변환 및 전처리 클래스"""
    def __init__(self):
        pass

    def shuffle_train_test_data(self, X_data, y_data, train_ratio=0.7, seed=None):
        self.seed = seed
        if seed is not None:
            random.seed(self.seed)

        combined_data = list(zip(X_data, y_data))

        # 데이터 섞기
        random.shuffle(combined_data)

        # 데이터 분리
        X_data, y_data = zip(*combined_data)

        # 학습/테스트 데이터 나누기
        split_index = int(len(X_data) * train_ratio)
        X_train = X_data[:split_index]
        y_train = y_data[:split_index]
        X_test = X_data[split_index:]
        y_test = y_data[split_index:]

        return X_train, y_train, X_test, y_test
    
    def flatten(self,data):
        """다차원 배열을 1차원으로 변환"""
        result = []
        for item in data:
            if isinstance(item, list):
                result.extend(self.flatten(item))
            else:
                result.append(item)
        return result

    def encode(self,labels):
        """라벨을 One-hot 인코딩"""
        num_classes = max(labels) + 1
        one_hot = []
        for label in labels:
            vector = [0] * num_classes
            vector[label] = 1
            one_hot.append(vector)
        return one_hot
    
    def scale_data(self,data_bundle): #매서드화
        scaled_data_bundle = []
        for data in data_bundle:
                
            data_min = min(data) #최솟값
            data_max = max(data) #최댓값
        
            if data_min == data_max:  #최대와 최소가 같을 경우 예외 처리
                return[0.5] * len(data)
            
            else:
                scaled_data = []     #스케일링 된 수를 넣는 리스트

                for k in data:       #데이터를 0과 1사이로 스케일링 하는 코드
                    scaled_value = (k - data_min) / (data_max - data_min) 
                    scaled_data.append(scaled_value)
            scaled_data_bundle.append(scaled_data)
        
        return scaled_data_bundle
